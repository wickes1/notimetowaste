"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { cn } from "@/lib/utils";
import { deleteTodo, updateTodo } from "@/server/todos/actions";
import { Todo } from "@/types/custom";
import { Trash2 } from "lucide-react";
import { useFormStatus } from "react-dom";
import { TodoOptimisticUpdate } from "./todo-list";

export function TodoItem({
	todo,
	optimisticUpdate
}: {
	todo: Todo;
	optimisticUpdate: TodoOptimisticUpdate;
}) {
	return (
		<form>
			<TodoCard optimisticUpdate={optimisticUpdate} todo={todo} />
		</form>
	);
}

export function TodoCard({
	todo,
	optimisticUpdate
}: {
	todo: Todo;
	optimisticUpdate: TodoOptimisticUpdate;
}) {
	const { pending } = useFormStatus();

	return (
		<Card className={cn("w-full", pending && "opacity-50")}>
			<CardContent className="flex items-start gap-3 p-3">
				<span className="size-10 flex items-center justify-center">
					<Checkbox
						// disabled={pending}
						type="submit"
						checked={Boolean(todo.is_complete)}
						formAction={async () => {
							optimisticUpdate({
								action: "update",
								todo: {
									...todo,
									is_complete: !todo.is_complete
								}
							});
							await updateTodo({
								...todo,
								is_complete: !todo.is_complete
							});
						}}
					/>
				</span>
				<p className={cn("flex-1 pt-2 min-w-0 break-words")}>
					{todo.task}
				</p>
				<Button
					// disabled={pending}
					formAction={async data => {
						optimisticUpdate({ action: "delete", todo });
						await deleteTodo(todo.id);
					}}
					variant="ghost"
					size="icon"
				>
					<Trash2 className="h-5 w-5" />
					<span className="sr-only">Delete Todo</span>
				</Button>
			</CardContent>
		</Card>
	);
}
