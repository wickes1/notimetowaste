import React from "react";
import ProductItem from "./ProductItem";
import { ApiProductProduct } from "../contentTypes";

function ProductList({ productList }: { productList: ApiProductProduct[] }) {
	return (
		<div className="mt-10">
			<h2 className="text-green-600 font-bold text-2xl">Product List</h2>
			<div
				className="grid
            grid-cols-2
            md:grid-cols-3
            lg:grid-cols-4
            gap-5 mt-6
            "
			>
				{productList.map((product, index) => (
					<ProductItem key={index} product={product} />
				))}
			</div>
		</div>
	);
}

export default ProductList;
