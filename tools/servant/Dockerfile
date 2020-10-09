FROM elixir:alpine

WORKDIR /usr/local/src/servant/
COPY mix.* .
RUN mix local.hex --force && \
        mix local.rebar --force && \
        mix deps.get && \
        mix deps.compile
COPY lib lib
RUN mix compile
EXPOSE 4000

CMD [ "mix", "run", "--no-halt" ]
