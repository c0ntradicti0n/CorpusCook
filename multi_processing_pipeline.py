import multiprocessing as mp

POISON_PILL = "STOP"

def stage1(q_in, q_out):

    while True:

        # get either work or a poison pill from the previous stage (or main)
        val = q_in.get()

        # check to see if we got the poison pill - pass it along if we did
        if val == POISON_PILL:
            q_out.put(val)
            return

        # do stage 1 work
        val = val + "Stage 1 did some work.\n"

        # pass the result to the next stage
        q_out.put(val)

def stage2(q_in, q_out):

    while True:

        val = q_in.get()
        if val == POISON_PILL:
            q_out.put(val)
            return

        val = val + "Stage 2 did some work.\n"
        q_out.put(val)

def main():

    pool = mp.Pool()
    manager = mp.Manager()

    # create managed queues
    q_main_to_s1 = manager.Queue()
    q_s1_to_s2 = manager.Queue()
    q_s2_to_main = manager.Queue()

    # launch workers, passing them the queues they need
    results_s1 = pool.apply_async(stage1, (q_main_to_s1, q_s1_to_s2))
    results_s2 = pool.apply_async(stage2, (q_s1_to_s2, q_s2_to_main))

    # Send a message into the pipeline
    q_main_to_s1.put("Main started the job.\n")

    # Wait for work to complete
    print(q_s2_to_main.get()+"Main finished the job.")

    q_main_to_s1.put(POISON_PILL)

    pool.close()
    pool.join()

    return

if __name__ == "__main__":
    main()