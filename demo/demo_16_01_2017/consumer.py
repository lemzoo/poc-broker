from broker.manage_worker import ManageWorker


if __name__ == '__main__':
    # Create Thread
    manager = ManageWorker()

    # Start the Thread
    manager.start()

    # Wait until the thread finish working
    manager.join()
