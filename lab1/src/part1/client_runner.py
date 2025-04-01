import subprocess
import time
import multiprocessing

start_time = time.perf_counter()


def run_script():
    subprocess.run(["python3", "client.py", '--host=127.0.0.1', '--stock=FishCo'])
    # time.sleep(1)


if __name__ == "__main__":

    procs = []

    for i in range(10):
        process = multiprocessing.Process(target=run_script)
        process.start()
        procs.append(process)
        

    for process in procs:
        process.join()

    end = time.perf_counter()

    print(end-start_time)

# for i in range(10):
#     # time.sleep(0.1)
#     subprocess.run(["python3", "client.py", '--stock=FishCo'])
#     latency = time.perf_counter() - start_time
#     print("Request " + str(i) + " latency : " +str(latency) + " seconds")
