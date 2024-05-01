"use client";
import { Button } from "@/components/ui/button";
import { oAuthSignIn } from "@/server/login/actions";
import { Provider } from "@supabase/supabase-js";
import { Github } from "lucide-react";

type OAuthProvider = {
	name: Provider;
	displayName: string;
	icon?: JSX.Element;
};

export function OAuthButtons() {
	const oAuthProvider: OAuthProvider[] = [
		{
			name: "github",
			displayName: "GitHub",
			icon: <Github className="size-5" />
		}
	];

	return (
		<>
			{oAuthProvider.map(provider => (
				<Button
					key={provider.name}
					variant="outline"
					className="w-full flex items-center justify-center gap-2"
					onClick={async () => {
						await oAuthSignIn(provider.name);
					}}
				>
					{provider.icon}
					<span className="ml-2">
						Login with {provider.displayName}
					</span>
				</Button>
			))}
		</>
	);
}
