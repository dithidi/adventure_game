import esbuild from 'esbuild';
import { globPlugin } from 'esbuild-plugin-glob';

esbuild.build({
    entryPoints: ['static/src/js/app.js'],
    outdir: 'static/dist/js',
    bundle: true,
    minify: true,
    sourcemap: true,
    plugins: [globPlugin()],
    define: {
        "process.env.NODE_ENV": JSON.stringify("development"),
    }
}).catch(() => process.exit(1))
