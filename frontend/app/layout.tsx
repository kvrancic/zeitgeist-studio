import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Zeitgeist Studio | AI Marketing Campaign Generator",
  description: "Transform trend analysis into complete, ready-to-deploy marketing campaigns in minutes, powered by multi-agent AI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
