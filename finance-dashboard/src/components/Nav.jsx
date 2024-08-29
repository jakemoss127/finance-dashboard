import React from "react";
import { RxTextAlignJustify } from "react-icons/rx";
import { RxPlus } from "react-icons/rx";
import { RxMagnifyingGlass } from "react-icons/rx";
import { FaToriiGate } from "react-icons/fa6";
import { FaMagnifyingGlass } from "react-icons/fa6";
import Pic from "../assets/moss.png";
export const Nav = () => {
  return (
    <div className="flex justify-between">
      <div className="flex gap-2">
        <div className="justify-center p-4 bg-white border border-zinc-100 rounded-full">
          <RxTextAlignJustify />
        </div>
        <div className="justify-center p-4 bg-black border border-zinc-100 rounded-full">
          <FaToriiGate className=" text-white" />
        </div>
        <div className="ml-4 flex flex-col font-semibold">
          <h1 className="text-large">Financial</h1>
          <h2 className="text-large font-normal">Dashboard</h2>
        </div>
        <div></div>
      </div>
      <div className="flex gap-2">
        <div className="justify-center p-4 bg-none border border-zinc-200 rounded-full">
          <RxPlus />
        </div>
        <div className="justify-center items-top pt-3 px-4 bg-black border border-zinc-200 rounded-full">
            <p className="items-top text-center text-large w-4 text-white font-bold max-h-4">J</p>
        </div>
        <div className="flex flex-col text-sm justify-center mr-16">
            <p className="font-semibold">
                John Snow
            </p>
            <p className="text-xs">
                CEO & Founder
            </p>
        </div>
        <div className="justify-center p-4 bg-none border border-zinc-200 rounded-full">
          <RxMagnifyingGlass />
        </div>
        <input
          className="bg-zinc-50 text-xs px-4 focus:outline-none"
          placeholder="Start searching here ..."
          type="text"
        ></input>
      </div>
    </div>
  );
};
