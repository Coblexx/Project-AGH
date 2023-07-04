import { MainNav } from "@/components/MainNav";

// import { DataTable } from "./CustomersPage/components/DataTable";
import { ColumnsOrders } from "./CustomersPage/components/ColumnsOrders";
import { UserNav } from "./CustomersPage/components/UserNav";
import { navigationLinks } from "../config/navigationLinks";
import { useEffect, useState } from "react";
import { data } from "autoprefixer";
import { TableOrders } from "./CustomersPage/components/TableOrders";

const ordersList = function () {
  const [orderData, setOrderData] = useState([]);

  const fetchData = () => {
    fetch("http://localhost:8000/customers/orders-list")
      .then((response) => response.json())
      .then((jsonData) => {
        // console.log(jsonData);
        const formatedData = jsonData.map((order) => ({
          name: order.customer_name,
          order_id: order.order_id,
          products_list: order.product_list.map(
            (product) => product.name + ", "
          ),
        }));
        setOrderData(formatedData);
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => fetchData(), []);
  return orderData;
};

export const OrdersPage = () => {
  const ordersData = ordersList();
  return (
    <div className="hidden flex-col md:flex">
      <div className="border-b">
        <div className="flex h-16 items-center px-4">
          <MainNav className="mx-6" links={navigationLinks} />
          <div className="ml-auto flex items-center space-x-4">
            <UserNav />
          </div>
        </div>
      </div>
      <div className="flex-1 space-y-4 p-8 pt-6">
        <div className="flex items-center justify-between space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">Orders</h2>
        </div>
        <div className="hidden h-full flex-1 flex-col space-y-8 md:flex">
          <TableOrders data={ordersData} columns={ColumnsOrders} />
        </div>
      </div>
    </div>
  );
};
