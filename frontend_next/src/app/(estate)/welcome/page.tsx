import React from "react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Condominio | Welcome",
  description:
    "Welcome to the Condominio Website. This webapp allows users who are tenants to signup, create their profiles, report any issues with their apartments, report any tenants, post anything of relevance for other tenants to see and or respond.",
};

export default function WelcomePage() {
  return (
    <div>
      <h1 className="dark:text-pumpkin text-6xl">Welcome</h1>
    </div>
  );
}
