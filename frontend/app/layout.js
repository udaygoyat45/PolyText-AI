import { Inter } from "next/font/google";
import Link from 'next/link';
import Image from 'next/image';
import "./globals.css";
import logoIcon from './logo.svg'

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "PolyText AI",
  description: "Next Gen AI",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className='flex flex-col'>
          <nav className="bg-zinc-100 border-gray-200 dark:bg-gray-900">
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
              <Link href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                <Image src={logoIcon} alt='PolyText Logo' height={40}/>
                <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">PolyText AI</span>
              </Link>
              <div className="hidden w-full md:block md:w-auto" id="navbar-default">
                <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-zinc-100 dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
                  <li>
                    <Link href="/" className="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500" aria-current="page">Home</Link>
                  </li>
                  <li>
                    <Link href="/about" className="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent">About</Link>
                  </li>
                </ul>
              </div>
            </div>
          </nav>

          {children}

          <footer className="bg-zinc-100 mt-auto rounded-lg shadow m-4 dark:bg-gray-800">
            <div className="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between">
              <span className="text-sm text-gray-500 sm:text-center dark:text-gray-400">© 2024 <Link href="/" className="hover:underline">PolyText™</Link>. All Rights Reserved.
              </span>

              <ul className="flex flex-wrap items-center mt-3 text-sm font-medium text-gray-500 dark:text-gray-400 sm:mt-0">
                <li>
                  <Link href='/about' className="hover:underline me-4 md:me-6">About</Link>
                </li>
                <li>

                  <Link href="https://hacklytics.io/">Made by Uday, Manas, Kunal, and Harish</Link>
                </li>
              </ul>
            </div>
          </footer>
        </div>
        </body>
    </html>
  );
}
