import { topCategoryStyles } from "@/constants";
import { cn } from "@/lib/utils";

import { Progress } from "./ui/progress";

const Category = ({ category }: CategoryProps) => {
  const {
    bg,
    circleBg,
    text: { main, count },
    progress: { bg: progressBg, indicator },
    icon,
  } = topCategoryStyles[category.name as keyof typeof topCategoryStyles] ||
  topCategoryStyles.default;

  return (
    <div className={cn("gap-[18px] flex p-4 rounded-xl", bg)}>
      <figure className={cn("flex-center size-10 rounded-full", circleBg)}>
        <img src={icon} width={20} height={20} alt={'onename'} />
      </figure>
      <div className="flex w-full flex-1 flex-col gap-2">
        <div className="text-14 flex justify-between">
          <h2 className={cn("font-medium", main)}>{"cate name"}</h2>
          <h3 className={cn("font-normal", count)}>{23}</h3>
        </div>
        <Progress
          value={(100 / 200) * 100}
          className={cn("h-2 w-full", progressBg)}
          // indicatorClassName="h-2 w-full"
        />
      </div>
    </div>
  );
};

export default Category;
