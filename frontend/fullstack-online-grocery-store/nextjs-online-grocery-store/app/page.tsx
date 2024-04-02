import Header from "./_components/Header";
import Sliders from "./_components/Sliders";
import GlobalApi from "./_utils/GlobalApi";
import CategoryList from "./_components/CategoryList";
import ProductList from "./_components/ProductList";
import Image from "next/image";
import Footer from "./_components/Footer";

export default async function Home() {
	const sliderList = await GlobalApi.getSliders();
	const categoryList = await GlobalApi.getCategoryList();
	const productList = await GlobalApi.getAllProducts();

	return (
		<div>
			<Header />
			<div className="p-5 md:p-10 px-16">
				<Sliders sliderList={sliderList} />
				<CategoryList categoryList={categoryList} />
				<ProductList productList={productList} />
				<Image
					src={"/banner.jpg"}
					alt="banner"
					width={1000}
					height={200}
					className="w-full h-[400px] object-cover mt-7"
				/>
				<Footer />
			</div>
		</div>
	);
}
