# Visualizer

<img alt="Kazimierz Nowak's bicycle"
     src="https://upload.wikimedia.org/wikipedia/commons/f/f6/Kazimierz_Nowak%27s_bicycle_2.jpg"
     align="right"
     width="448px"
/>

The visualizer is a simple tool for visualizing the produced predictions in the browser.

## Development

All you need is Emacs ([*The One True Editor*](https://stallman.org/saintignucius.jpg)) and Cider. Start the REPL with `M-x cider-jack-in-cljs`, choose `shadow` as the ClojureScript REPL type and `visualizer` as the build.

Now the code is sent to the browser from the REPL. You can test it by running `(js/alert "hello world")` in the REPL.

## Production build

```
$ npx shadow-cljs release visualizer
```
