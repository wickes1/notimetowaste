import { TodoList } from "@/components/todo-list";
import { Separator } from "@/components/ui/separator";
import { Todo } from "@/types/custom";
import { createClient } from "@/utils/supabase/server";
import { redirect } from "next/navigation";

export default async function TodosPage() {
	const supabase = createClient();

	// if user is not logged in, redirect to login page
	const { data, error } = await supabase.auth.getUser();
	if (!data?.user) {
		redirect("/login");
	}

	const { data: todos } = await supabase
		.from("todos")
		.select()
		.order("inserted_at", { ascending: false });

	return (
		<section className="p-3 pt-6 max-w-2xl w-full flex flex-col gap-4">
			<h1 className="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
				Todo&apos;s
			</h1>
			<Separator className="w-full " />
			<TodoList todos={todos ?? []} />
		</section>
	);
}
