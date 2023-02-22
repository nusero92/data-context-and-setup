import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you
        # have access to the instance of the class Order in the variable self,
        # as well as all its attributes

       #make sure to create a copy rather than a "view"
        orders=self.data["orders"].copy()

        # filter out non delivered orders
        orders=orders[orders["order_status"]=="delivered"]

        #change object to datetime format
        orders["order_purchase_timestamp"]=pd.to_datetime(orders["order_purchase_timestamp"])
        orders.loc[:,"order_approved_at"]=pd.to_datetime(orders["order_approved_at"])
        orders.loc[:,"order_delivered_carrier_date"]=pd.to_datetime(orders["order_delivered_carrier_date"])
        orders.loc[:,"order_delivered_customer_date"]=pd.to_datetime(orders["order_delivered_customer_date"])
        orders.loc[:,"order_estimated_delivery_date"]=pd.to_datetime(orders["order_estimated_delivery_date"])

        #compute Wait_time, expected_wait_time, delay_vs_expected
        a=orders["order_purchase_timestamp"]
        b=orders["order_delivered_customer_date"]
        diff=(b-a)/np.timedelta64(24,"h")
        orders["wait_time"]=diff


        a=orders["order_purchase_timestamp"]
        b=orders["order_estimated_delivery_date"]
        diff=(b-a)/np.timedelta64(24,"h")
        orders["expected_wait_time"]=diff


        a=orders["order_estimated_delivery_date"]
        b=orders["order_delivered_customer_date"]
        diff=(b-a)/np.timedelta64(24,"h")
        orders["delay_vs_expected"]=diff

        def handle_delay(x):
            if x > 0:
                return x
            else:
                return 0

        orders.loc[:,'delay_vs_expected'] = orders['delay_vs_expected'].apply(handle_delay)

        #asseble the new df
        orders_wait_time = orders[['order_id', 'wait_time', 'expected_wait_time',
                                     'delay_vs_expected', 'order_status']]

        return orders_wait_time


    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews=self.data["order_reviews"].copy()

        dim_is_one_star = lambda x: int(x==1)
        dim_is_five_star = lambda x: int(x==5)

        reviews["dim_is_five_star"] = reviews["review_score"].map(dim_is_five_star) # --> Series([0, 1, 1, 0, 0, 1 ...])
        reviews["dim_is_one_star"] = reviews["review_score"].map(dim_is_one_star) # --> Series([0, 1, 1, 0, 0, 1 ...])

        reviews_new=reviews[["order_id", "dim_is_five_star", "dim_is_one_star", "review_score"]]
        return reviews_new

    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        items_df_copy=self.data["order_items"].copy()

        items_groupt=items_df_copy[["order_id","order_item_id"]].groupby("order_id").count()
        items_rename=items_groupt.rename(columns={"order_item_id": "number_of_products"})
        items_sort=items_rename.sort_values("number_of_products")
        items=items_sort.reset_index()
        return items

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        sellers=self.data["order_items"].copy()
        sellers=sellers.groupby('order_id')['seller_id'].nunique().reset_index()
        sellers.columns = ['order_id', 'number_of_sellers']
        sellers.sort_values('number_of_sellers')
        return sellers
    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        price_freight_copy=self.data["order_items"]

        group=price_freight_copy[["order_id","price","freight_value"]].groupby('order_id',
             as_index=False)
        price_freight=group.agg({'price': 'sum',
                                  'freight_value': 'sum'})
        return price_freight

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        matching_geo = Order().get_distance_seller_customer()
        return matching_geo

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        pass  # YOUR CODE HERE
