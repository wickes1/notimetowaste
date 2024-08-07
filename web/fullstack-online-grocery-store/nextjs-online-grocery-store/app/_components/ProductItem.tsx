import Image from "next/image";
import React from "react";
import { ApiProductProduct } from "../contentTypes";
import { Button } from "@/components/ui/button";

function ProductItem({ product }: { product: ApiProductProduct }) {
	return (
		<div
			className="p-2 md:p-6
        flex flex-col items-center
        justify-center gap-3 rounded-lg border
        hover:scale-105 hover:shadow-md transition-all ease-in-out cursor-pointer
        "
		>
			<Image
				src={
					process.env.NEXT_PUBLIC_BACKEND_BASE_URL +
					product.attributes?.images?.data[0]?.attributes?.url
				}
				alt={product.attributes.name}
				width={500}
				height={200}
				className="h-[200px] w-[200px] object-contain"
			/>
			<h2 className="font-bold text-lg">{product.attributes.name}</h2>
			<div className="flex gap-3">
				{product.attributes.sellingPrice && (
					<h2 className="font-bold text-lg">
						${product.attributes.sellingPrice}
					</h2>
				)}
				<h2
					className={`font-bold  text-lg ${
						product.attributes.sellingPrice &&
						"line-through text-gray-500"
					}`}
				>
					${product.attributes.mrp}
				</h2>
			</div>
			<Button
				variant={"outline"}
				className="text-primary hover:text-white hover:bg-primary"
			>
				Add to cart
			</Button>
		</div>
	);
}

export default ProductItem;
