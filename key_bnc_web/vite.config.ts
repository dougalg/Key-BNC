/// <reference types="vitest/config" />
import path from "path";
import { defineConfig, loadEnv, UserConfig } from "vite";
import { playwright } from "@vitest/browser-playwright";
import vue from "@vitejs/plugin-vue";
import legacy from "@vitejs/plugin-legacy";
import { VitePWA } from "vite-plugin-pwa";
import plainText from "vite-plugin-virtual-plain-text";
import { GitRevisionPlugin } from "git-revision-webpack-plugin";
import tsconfigPaths from "vite-tsconfig-paths";
import wasmPack from "vite-plugin-wasm-pack";
import { changelogPlugin } from "./tools/vite/changelogPlugin";

const gitRevisionPlugin = new GitRevisionPlugin({
	versionCommand: "describe --always --tags",
});

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, "");

	const htmlPlugin = () => {
		return {
			name: "html-transform",
			transformIndexHtml(html: string) {
				return html.replace(/%(.*?)%/g, function (match, p1) {
					return env[p1];
				});
			},
		};
	};

	return {
		plugins: [
			vue(),
			legacy({
				targets: ["defaults", "not dead", "> 1%", "last 2 versions"],
			}),
			VitePWA({
				workbox: {
					maximumFileSizeToCacheInBytes: 9_000_000, // 9MB
				},
			}),
			plainText(),
			tsconfigPaths({}),
			wasmPack.default("./key_bnc_wasm"),
			htmlPlugin(),
			changelogPlugin({ logFile: path.resolve(__dirname, "../CHANGELOG.md") }),
		],
		define: {
			__APP_VERSION__: `"${gitRevisionPlugin.version()}"`,
		},
		resolve: {
			alias: [
				{
					find: "@",
					replacement: path.resolve("src"),
				},
			],
		},
		test: {
			browser: {
				enabled: true,
				provider: playwright(),
				instances: [{ browser: "chromium" }],
			},
			coverage: {
				provider: "v8",
				include: ["src/**/*{.ts,.vue}"],
				thresholds: {
					statements: 5.95,
					functions: 5.48,
					branches: 5.41,
					lines: 5.66,
				},
			},
		},
	} satisfies UserConfig;
});
