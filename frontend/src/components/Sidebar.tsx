"use client";

import { sidebarLinks } from "@/constants";
import { cn } from "@/lib/utils";
import Footer from "./Footer";
import { Link } from "react-router-dom";
// import PlaidLink from './PlaidLink'

const Sidebar = () => {
  const pathname = window.location.pathname;

  return (
    <section className="sidebar">
      <nav className="flex flex-col gap-4">
        <a
          href="/dashboard"
          className="mb-12 cursor-pointer flex items-center gap-2"
        >
          <img
            src="/logo.svg"
            width={34}
            height={34}
            alt="Lilbex logo"
            className="size-[24px] max-xl:size-14"
          />
          <h1 className="sidebar-logo">Lilbex</h1>
        </a>

        {sidebarLinks.map((item) => {
          const isActive =
            pathname === item.route || pathname.startsWith(`${item.route}/`);

          return (
            <Link
              to={item.route}
              key={item.label}
              className={cn("sidebar-link", { "bg-bank-gradient": isActive })}
            >
              <div className="relative size-6">
                <img
                  src={item.imgURL}
                  alt={item.label}
                  className={cn({
                    "brightness-[3] invert-0": isActive,
                  })}
                />
              </div>
              <p className={cn("sidebar-label", { "!text-white": isActive })}>
                {item.label}
              </p>
            </Link>
          );
        })}

        {/* <PlaidLink user={user} /> */}
      </nav>

      <Footer />
    </section>
  );
};

export default Sidebar;
