import type { Metadata } from "next";
import Image from "next/image";
import buildings from "@/../public/assets/images/buildings.webp";
import Link from "next/link";
import { ArrowRightIcon } from "@heroicons/react/24/solid";

export const metadata: Metadata = {
  title: "Home | Condominio",
  description: "Condominio. Crie uma conta para começar",
};

export default function HomePage() {
  return (
    <div className="relative h-screen">
      <div className="absolute inset-0 z-0">
        <Image
          src={buildings}
          alt="Apartments"
          fill
          style={{ objectFit: "cover", objectPosition: "center" }}
          priority
        />
      </div>
      <main className="flex-center relative z-10 h-full bg-black/50">
        <div className="text-center">
          <div className="font-robotoSlab mb-4 text-4xl font-semibold text-cyan-400 antialiased sm:text-6xl md:text-8xl">
            Welcome to Condominio
          </div>
          <p className="my-8 text-2xl text-teal-300 sm:text-4xl">
            Are you a tenant? or an existing tenant?
          </p>
          <Link href="/register" prefetch={false}>
            <button className="bg-asparagus rounded-3xl px-4 py-2 text-lg font-semibold text-white hover:bg-lime-700 sm:px-6 sm:text-2xl">
              <span className="inline-flex items-center">
                Create Your Account
                <ArrowRightIcon className="ml-2 size-8" />
              </span>
            </button>
          </Link>
        </div>
      </main>
    </div>
  );
}
