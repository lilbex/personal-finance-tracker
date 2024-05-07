import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import React, { useState } from "react";
// import { BankTabItem } from "./BankTabItem";
// import BankInfo from "./BankInfo";
// import TransactionsTable from "./TransactionsTable";
// import { Pagination } from "./Pagination";
import { cn } from "@/lib/utils";

const RecentTransactions = () => {
  const [isActive, setIsActive] = useState<String>("account");
  return (
    <section className="recent-transactions">
      <header className="flex items-center justify-between">
        <h2 className="recent-transactions-label">Recent transactions</h2>
        <a href={`/transaction-history/?id=`} className="view-all-btn">
          View all
        </a>
      </header>

      <Tabs defaultValue="account" className="w-full">
        <TabsList className="recent-transactions-tablist">
          <TabsTrigger value="account">
            <div
              onClick={() => setIsActive("account")}
              className={cn(`banktab-item`, {
                " border-blue-600": isActive === "account",
              })}
            >
              <p
                className={cn(
                  `text-16 line-clamp-1 flex-1 font-medium text-gray-500`,
                  {
                    " text-blue-600": isActive === "account",
                  }
                )}
              >
                Account
              </p>
            </div>
          </TabsTrigger>
          <TabsTrigger value="password">
            <div
              onClick={() => setIsActive("password")}
              className={cn(`banktab-item`, {
                " border-blue-600": isActive === "password",
              })}
            >
              <p
                className={cn(
                  `text-16 line-clamp-1 flex-1 font-medium text-gray-500`,
                  {
                    " text-blue-600": isActive === "password",
                  }
                )}
              >
                Password
              </p>
            </div>
          </TabsTrigger>
        </TabsList>
        <TabsContent value="account">
          Make changes to your account here.
        </TabsContent>
        <TabsContent value="password">Change your password here.</TabsContent>
      </Tabs>
    </section>
  );
};

export default RecentTransactions;
