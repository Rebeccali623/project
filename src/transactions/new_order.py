from datetime import datetime


def new_order_input_helper(lines):
    items = []
    for line in lines:
        info = line.strip().split(",")
        items.append(OrderItem(int(info[0]), int(info[1]), int(info[2])))
    return items


class OrderItem:
    def __init__(self, item_id, supplier_id, quantity, price=0, name='', stock_quantity=0):
        self.Id = item_id
        self.supplier_id = supplier_id
        self.quantity = quantity
        self.price = price
        self.name = name
        self.stock_quantity = stock_quantity


class NewOrderHandler:
    def __init__(self, session, c_id, w_id, d_id, n_item):

        self.session = session
        self.c_id = int(c_id)
        self.w_id = int(w_id)
        self.d_id = int(d_id)
        self.n_item = int(n_item)

    def run(self, lines):
        items = new_order_input_helper(lines)

        # step 1
        N = self.session.execute(
            '''
            SELECT d_next_o_id 
            FROM CS5424sample.sample_district 
            WHERE d_w_id = {} AND d_id = {};
            '''.format(self.w_id, self.d_id)).one()
        N = int(N.d_next_o_id)

        # step 2
        self.session.execute(
            '''
            UPDATE CS5424sample.sample_district 
            SET d_next_o_id = d_next_o_id + 1 
            WHERE d_w_id = {} AND d_id = {};
            '''.format(self.w_id, self.d_id))

        # step 3
        all_local = 1
        for item in items:
            if item.supplier_id != self.w_id:
                all_local = 0
                break

        t = "'" + str(datetime.now())[:-3] + "'"

        self.session.execute(
            '''
            INSERT INTO CS5424sample.sample_order (o_w_id,o_d_id,o_id,o_c_id,o_carrier_id,o_ol_cnt,o_all_local,o_entry_d) 
            VALUES ({},{},{},{},{},{},{},{})
            '''.format(self.w_id, self.d_id, N, self.c_id, 'null', self.n_item, all_local, t))

        # step 4
        total_amount = 0

        # step 5
        for i in range(len(items)):
            item = items[i]
            stock = self.session.execute(
                '''
                SELECT * 
                FROM CS5424sample.sample_stock 
                WHERE s_w_id = {} AND s_i_id = {}
                '''.format(item.supplier_id, item.Id)).one()
            # 5a
            s_quantity = stock.s_quantity
            # 5b
            adjusted_quantity = s_quantity - item.quantity
            # 5c
            if adjusted_quantity < 10:
                adjusted_quantity += 100
            remote_cnt = 0
            if item.supplier_id != self.w_id:
                remote_cnt = 1
            # 5d
            self.session.execute(
                '''
                UPDATE CS5424sample.sample_stock
                SET s_quantity = {}, s_ytd = s_ytd+{}, s_order_cnt = s_order_cnt+1, s_remote_cnt = s_remote_cnt+{}
                WHERE s_w_id = {} AND s_i_id = {};
                '''.format(adjusted_quantity, item.quantity, remote_cnt, item.supplier_id, item.Id))
            # 5e
            item_row = self.session.execute(
                '''SELECT * 
                    FROM CS5424sample.sample_item 
                    WHERE i_id = {};
                '''.format(item.Id)).one()
            item.price = round(item_row.i_price, 2)
            item.name = item_row.i_name
            item.stock_quantity = adjusted_quantity
            item_amount = item.quantity * item.price

            # 5f
            total_amount += item_amount
            # 5g
            dist = "'S_DIST_" + str(self.d_id) + "'"
            s = """
            INSERT INTO CS5424sample.sample_order_line (ol_w_id,ol_d_id,ol_o_id,ol_number,ol_i_id,ol_delivery_d,
            ol_amount,ol_supply_w_id,ol_quantity,ol_dist_info) 
            VALUES ({}, {}, {},{},{},{},{},{},{},{});
            """.format(self.w_id, self.d_id, N, i, item.Id, 'null', item_amount, item.supplier_id, item.quantity, dist)
            self.session.execute(s)


        # step 6
        district_row = self.session.execute(
            '''
            SELECT * 
            FROM CS5424sample.sample_district 
            WHERE d_w_id = {} AND d_id = {};
            '''.format(self.w_id, self.d_id)).one()
        d_tax = round(district_row.d_tax, 4)
        warehouse_row = self.session.execute(
            '''
            SELECT * 
            FROM CS5424sample.sample_warehouse 
            WHERE w_id = {};
            '''.format(self.w_id)).one()
        w_tax = round(warehouse_row.w_tax, 4)
        customer_row = self.session.execute(
            '''
            SELECT * 
            FROM CS5424sample.sample_customer 
            WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};'''.format(self.w_id, self.d_id, self.c_id)).one()
        c_discount = round(customer_row.c_discount, 4)

        total_amount = total_amount * (1 + d_tax + w_tax) * (1 - c_discount)

        # output
        out = '''customer: W_ID = {}, D_ID = {}, C_ID = {}, C_LAST = {}, C_CREDIT = {}, C_DISCOUNT = {}'''\
            .format(self.w_id, self.d_id, self.c_id, customer_row.c_last, customer_row.c_credit, c_discount)
        print(out)
        print("W_TAX = {}, D_TAX = {}".format(w_tax, d_tax))
        print("O_ID = {}, O_ENTRY_D = {}".format(N, t))
        print("NUM_ITEMS = {}, TOTAL_AMOUNT = {}".format(self.n_item, total_amount))
        for item in items:
            item_str = "ITEM_NUMBER = {}," \
                       "I_NAME = {}, " \
                       "SUPPLIER_WAREHOUSE = {}, " \
                       "QUANTITY = {}, " \
                       "OL_AMOUNT = {}, " \
                       "S_QUANTITY = {}".format(item.Id,
                                                item.name,
                                                item.supplier_id,
                                                item.quantity,
                                                item.price * item.quantity,
                                                item.stock_quantity)
            print(item_str)
