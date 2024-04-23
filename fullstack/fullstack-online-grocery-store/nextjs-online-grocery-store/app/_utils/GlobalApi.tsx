const { default: axios } = require("axios");

const axiosClient = axios.create({
	baseURL: process.env.NEXT_PUBLIC_BACKEND_BASE_URL
});

const getCategory = () => axiosClient.get("/api/categories?populate=*");

const getSliders = () =>
	axiosClient
		.get("/api/sliders?populate=*")
		.then((resp: { data: { data: any } }) => resp.data.data);

const getCategoryList = () =>
	axiosClient
		.get("/api/categories?populate=*")
		.then((resp: { data: { data: any } }) => resp.data.data);

const getAllProducts = () =>
	axiosClient
		.get("/api/products?populate=*")
		.then((resp: { data: { data: any } }) => resp.data.data);

const GlobalApi = { getCategory, getSliders, getCategoryList, getAllProducts };

export default GlobalApi;
