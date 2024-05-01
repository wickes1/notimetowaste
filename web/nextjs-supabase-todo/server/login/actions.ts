"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { createClient } from "@/utils/supabase/server";

export async function emailLogin(formData: FormData) {
	const supabase = createClient();

	// type-casting here for convenience
	// in practice, you should validate your inputs
	const data = {
		email: formData.get("email") as string,
		password: formData.get("password") as string
	};

	const { error } = await supabase.auth.signInWithPassword(data);

	if (error) {
		redirect("/login?message=Invalid email or password");
	}

	revalidatePath("/", "layout");
	redirect("/todos");
}

export async function singUp(formData: FormData) {
	const supabase = createClient();

	// type-casting here for convenience
	// in practice, you should validate your inputs
	const data = {
		email: formData.get("email") as string,
		password: formData.get("password") as string
	};

	const { error } = await supabase.auth.signUp(data);

	if (error) {
		redirect("/login?message=An error occurred while signing up");
	}

	revalidatePath("/", "layout");
	redirect("/login");
}

export async function signOut() {
	const supabase = createClient();
	await supabase.auth.signOut();
	redirect("/login");
}
