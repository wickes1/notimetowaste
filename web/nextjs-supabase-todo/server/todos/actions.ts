"use server";

import { createClient } from "@/utils/supabase/server";
import { revalidatePath } from "next/cache";

export async function addTodo(formData: FormData) {
	const supabase = createClient();
	const text = formData.get("todo") as string | null;

	if (!text) {
		throw new Error("Todo cannot be empty");
	}

	const { data } = await supabase.auth.getUser();

	if (!data?.user) {
		throw new Error("User not logged in");
	}

	const { error } = await supabase.from("todos").insert([
		{
			task: text,
			user_id: data.user.id
		}
	]);

	if (error) {
		throw new Error("An error occurred while adding todo");
	}

	revalidatePath("/todos");
}
