import HeaderBox from "@/components/HeaderBox";
import RecentTransactions from "@/components/RecentTransactions";
import RightSidebar from "@/components/RightSidebar";
import TotalBalanceBox from "@/components/TotalBalanceBox";
import DashaboardLayout from "./dashboardLayout";

const Home = () => {
  return (
    <DashaboardLayout>
      <section className="home">
        <div className="home-content">
          <header className="home-header">
            <HeaderBox
              type="greeting"
              title="Welcome"
              user={"Guest"}
              subtext="Access and manage your account and transactions efficiently."
            />

            <TotalBalanceBox />
          </header>

          <RecentTransactions
          //   accounts={accountsData}
          //   transactions={account?.transactions}
          //   appwriteItemId={appwriteItemId}
          //   page={currentPage}
          />
        </div>

        <RightSidebar
        // user={loggedIn}
        // transactions={account?.transactions}
        // banks={accountsData?.slice(0, 2)}
        />
      </section>
    </DashaboardLayout>
  );
};

export default Home;
