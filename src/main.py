from transactions import new_order,payment
from cassandra.cluster import Cluster


def main():
    cluster = Cluster(['192.168.51.10'], 9043)
    session = cluster.connect()

    f = open("processed_files/sample/query.txt", "r")
    lines = f.readlines()
    f.close()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        args = line.split(",")
        command = args[0]
        if command == 'N':
            new_order_handler = new_order.NewOrderHandler(session, *args[1:])
            new_order_handler.run(lines[i+1: i+int(args[-1])+1])
            i += int(args[-1]) + 1
            continue
        elif command == 'P':
            payment_handler = payment.PaymentHandler(session, *args[1:])
            payment_handler.run()
            i += 1
            continue


if __name__ == "__main__":
    main()
