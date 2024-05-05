import AuthForm from "@/components/AuthForm";
import AuthLayout from "./authLayout";

const SignUp = () => {
  return (
    <AuthLayout>
      <section className="flex-center size-full max-sm:px-6">
        <AuthForm type="sign-up" />
      </section>
    </AuthLayout>
  );
};

export default SignUp;
