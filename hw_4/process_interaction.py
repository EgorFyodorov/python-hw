import multiprocessing
import time
import codecs
import sys
import traceback
from datetime import datetime

def process_a(queue_in, pipe_writer):
    while True:
        try:
            msg = queue_in.get()
            if msg == "STOP":
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} - A received STOP")
                pipe_writer.close()
                return
            
            processed_msg = msg.lower()
            
            time.sleep(5)
            
            pipe_writer.send(processed_msg)
        except Exception as e:
            print(f"Error in A: {e}")
            break

def process_b(pipe_reader, queue_out):
    while True:
        try:
            if pipe_reader.poll(1): 
                msg = pipe_reader.recv()
                
                encoded_msg = codecs.encode(msg, 'rot_13')
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} - B output: {encoded_msg}")
                sys.stdout.flush()
                
                queue_out.put(encoded_msg)
        except EOFError:
            print("B pipe closed")
            break
        except Exception as e:
            print(f"Error in B: {e}")
            break

def main():
    queue_a = multiprocessing.Queue()
    queue_out = multiprocessing.Queue()

    pipe_reader, pipe_writer = multiprocessing.Pipe(duplex=False)
    
    p_a = multiprocessing.Process(target=process_a, args=(queue_a, pipe_writer))
    p_b = multiprocessing.Process(target=process_b, args=(pipe_reader, queue_out))
    
    p_a.start()
    p_b.start()
    
    messages = ["Hello World", "Python", "Multiprocessing"]
    log_entries = []
    
    for msg in messages:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Main sent: {msg}"
        print(log_entry)
        log_entries.append(log_entry)
        queue_a.put(msg)

    queue_a.put("STOP")
    
    expected_responses = len(messages)
    received = 0
    start_wait = time.time()
    
    while received < expected_responses:
        try:
            resp = queue_out.get(timeout=10)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} - Main received: {resp}"
            print(log_entry)
            log_entries.append(log_entry)
            received += 1
        except Exception:
            if time.time() - start_wait > 40:
                print("Global timeout reached")
                break
    
    p_a.join()
    p_b.terminate()
    p_b.join()
    
    with open("artifacts/4.3.txt", "w") as f:
        f.write("\n".join(log_entries))

if __name__ == "__main__":
    main()
