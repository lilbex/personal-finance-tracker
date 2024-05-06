import React from "react";

const Footer = ({ type = "desktop" }: FooterProps) => {
  const handleLogOut = async () => {
    console.log("logout");
  };

  return (
    <footer className="footer">
      <div className={type === "mobile" ? "footer_name-mobile" : "footer_name"}>
        <p className="text-xl font-bold text-gray-700">E</p>
      </div>

      <div
        className={type === "mobile" ? "footer_email-mobile" : "footer_email"}
      >
        <h1 className="text-14 truncate text-gray-700 font-semibold">Elias</h1>
        <p className="text-14 truncate font-normal text-gray-600">
          elias@gmail.com
        </p>
      </div>

      <div className="footer_image" onClick={handleLogOut}>
        <img src="/logout.svg" alt="jsm" />
      </div>
    </footer>
  );
};

export default Footer;
