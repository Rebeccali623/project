class PaymentHandler:
    def __init__(self, session, w_id, d_id, c_id, payment):
        self.session = session
        self.w_id = int(w_id)
        self.d_id = int(d_id)
        self.c_id = int(c_id)
        self.payment = round(float(payment), 2)

    def run(self):
        # step 1
        print(self.payment)
        self.session.execute(
            '''
            UPDATE CS5424sample.sample_warehouse 
            SET w_ytd = w_ytd + {}
            WHERE w_id = {};
            '''.format(self.payment, self.w_id))

        warehouse_row = self.session.execute(
            '''
            SELECT *
            FROM CS5424sample.sample_warehouse
            WHERE w_id = {};
            '''.format(self.w_id)).one()
        # print(warehouse_row)

        # step 2
        self.session.execute(
            '''
            UPDATE CS5424sample.sample_district 
            SET d_ytd = d_ytd + {} 
            WHERE d_w_id = {} AND d_id = {};
            '''.format(self.payment, self.w_id, self.d_id))

        district_row = self.session.execute(
            '''
            SELECT *
            FROM CS5424sample.sample_district
            WHERE d_w_id = {} AND d_id = {};
            '''.format(self.w_id, self.d_id)).one()
        # print(district_row)

        # step 3
        self.session.execute(
            '''
            UPDATE CS5424sample.sample_customer 
            SET c_balance = c_balance + {}, c_ytd_payment = c_ytd_payment + {}, c_payment_cnt = c_payment_cnt + 1
            WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};
            '''.format(self.payment, self.payment, self.w_id, self.d_id, self.c_id))
        customer_row = self.session.execute(
            '''
            SELECT * 
            FROM CS5424sample.sample_customer 
            WHERE c_w_id = {} AND c_d_id = {} AND c_id = {};'''.format(self.w_id, self.d_id, self.c_id)).one()

        print(customer_row)

        # Output
        customer_output = '''
        customer: W_ID = {}, D_ID = {}, C_ID = {}, C_FIRST = {}, C_MIDDLE = {}, C_LAST = {}, C_STREET_1 = {}, 
        C_STREET_2 = {}, C_CITY = {}, C_STATE = {}, C_ZIP = {}, C_PHONE, C_SINCE = {}, C_CREDIT = {}, C_CREDIT_LIM = {}, 
        C_DISCOUNT = {}, C_BALANCE = {}
        '''.format(customer_row.c_w_id, customer_row.c_d_id, customer_row.c_id, customer_row.c_first,
                   customer_row.c_middle,customer_row.c_last,
                   customer_row.c_street_1, customer_row.c_street_2, customer_row.c_city, customer_row.c_state,
                   customer_row.c_zip, customer_row.c_phone, customer_row.c_since, customer_row.c_credit,
                   customer_row.c_credit_lim, customer_row.c_discount, customer_row.c_balance - self.payment)

        print(customer_output)

        warehouse_address = "W_STREET_1 = {}, W_STREET_2 = {}, W_CITY = {}, W_STATE = {}, W_ZIP = {}".format(
            warehouse_row.w_street_1, warehouse_row.w_street_2, warehouse_row.w_city, warehouse_row.w_state,
            warehouse_row.w_zip)

        print(warehouse_address)

        district_address = "D_STREET_1 = {}, D_STREET_2 = {}, W_CITY = {}, W_STATE = {}, W_ZIP = {}".format(
            district_row.d_street_1, district_row.d_street_2, district_row.d_city, district_row.d_state,
            district_row.d_zip)

        print(district_address)

        print("payment = {}".format(self.payment))
