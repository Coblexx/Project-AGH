import { MainNav } from "@/components/MainNav";

// import { DataTable } from "./CustomersPage/components/DataTable";
import { ProductColumns } from "./CustomersPage/components/ProductColumns";
import { UserNav } from "./CustomersPage/components/UserNav";
import { navigationLinks } from "../config/navigationLinks";
import { useEffect, useState } from "react";
import { data } from "autoprefixer";
import { TableProducts } from "./CustomersPage/components/TableProducts";

const productsListItems = function () {
  const [productsData, setproductsData] = useState([]);

  const fetchData = () => {
    fetch("http://localhost:8000/products")
      .then((response) => response.json())
      .then((jsonData) => {
        console.log(typeof jsonData);
        const formatedData = jsonData.map((product) => ({
          id: product.id,
          name: product.name,
          price: product.price,
        }));
        setproductsData(formatedData);
        // console.log(formatedData);
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => fetchData(), []);
  return productsData;
};

export const ProductsPage = () => {
  const productsData = productsListItems();
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
          <h2 className="text-3xl font-bold tracking-tight">Products</h2>
        </div>
        <div className="hidden h-full flex-1 flex-col space-y-8 md:flex">
          <TableProducts data={productsData} columns={ProductColumns} />
        </div>
      </div>
    </div>
  );
};
