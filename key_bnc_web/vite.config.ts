import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import legacy from '@vitejs/plugin-legacy';
import { VitePWA } from 'vite-plugin-pwa';
import plainText from 'vite-plugin-virtual-plain-text';
import { GitRevisionPlugin } from 'git-revision-webpack-plugin';
import tsconfigPaths from 'vite-tsconfig-paths';
import wasmPack from 'vite-plugin-wasm-pack';

const gitRevisionPlugin = new GitRevisionPlugin({
	versionCommand: 'describe --always --tags',
})

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
	}

	return {
		plugins: [
			vue(),
			legacy({
				targets: ['defaults', 'not dead', '> 1%', 'last 2 versions'],
			}),
			VitePWA(),
			plainText(),
			tsconfigPaths({
				extensions: [ '.ts', '.tsx', '.js', '.jsx', '.mjs', '.vue', '.wasm'],
			}),
			wasmPack(['./key_bnc_wasm']),
			htmlPlugin(),
		],
		define: {
			__APP_VERSION__: `"${gitRevisionPlugin.version()}"`,
		},
		resolve: {
			alias: [ {
				find: '@',
				replacement: path.resolve('src'),
			} ],
		},
	}
})
