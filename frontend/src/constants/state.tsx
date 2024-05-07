import {
  RecoilRoot,
  atom,
  selector,
  useRecoilState,
  useRecoilValue,
} from "recoil";

export const todoListState = atom({
  key: "TodoList",
  default: [],
});
