// import Image from "next/image";
// import Link from "next/link";
import React from "react";
import BankCard from "./BankCard";
// import { countTransactionCategories } from "@/lib/utils";
// import Category from "./Category";

const RightSidebar = () => {
  // const categories: CategoryCount[] = countTransactionCategories(transactions);

  const banks = [
    {
      name: "Elias",
      currentBalance: 3000,
      mask: true,
      sharaebleId: "iisoiosd",
    },
    {
      name: "Elias",
      currentBalance: 3000,
      mask: true,
      sharaebleId: "iisoiosd",
    },
  ];

  return (
    <aside className="right-sidebar">
      <section className="flex flex-col pb-8">
        <div className="profile-banner" />
        <div className="profile">
          <div className="profile-img">
            <span className="text-5xl font-bold text-blue-500">E</span>
          </div>

          <div className="profile-details">
            <h1 className="profile-name">elias imokhai</h1>
            <p className="profile-email">eliasimokhai@gmail.com</p>
          </div>
        </div>
      </section>

      <section className="banks">
        <div className="flex w-full justify-between">
          <h2 className="header-2">My Banks</h2>
          <a href="/" className="flex gap-2">
            <img src="/plus.svg" width={20} height={20} alt="plus" />
            <h2 className="text-14 font-semibold text-gray-600">Add Bank</h2>
          </a>
        </div>

        {banks?.length > 0 && (
          <div className="relative flex flex-1 flex-col items-center justify-center gap-5">
            <div className="relative z-10">
              <BankCard
              // key={1}
              // account={banks[0]}
              // userName={`elias imoklhai`}
              // showBalance={false}
              />
            </div>
            {banks[1] && (
              <div className="absolute right-0 top-8 z-0 w-[90%]">
                <BankCard
                // key={2}
                // account={banks[1]}
                // userName={`Elias imokahi`}
                // showBalance={false}
                />
              </div>
            )}
          </div>
        )}

        <div className="mt-10 flex flex-1 flex-col gap-6">
          <h2 className="header-2">Top categories</h2>

          <div className="space-y-5">
            {/* {categories.map((category, index) => (
              <Category key={category.name} category={category} />
            ))} */}
          </div>
        </div>
      </section>
    </aside>
  );
};

export default RightSidebar;
