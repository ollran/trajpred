defmodule Servant.Router do
  # https://hexdocs.pm/plug/Plug.Router.html

  use Plug.Router
  require Logger

  plug(:match)
  plug(:dispatch)

  get("/", do: send_resp(conn, 200, "found"))
  match(_, do: send_resp(conn, 404, "not found"))

  def child_spec(opts),
    do: %{
      id: __MODULE__,
      start: {__MODULE__, :start_link, [opts]},
      type: :worker,
      restart: :permanent,
      shutdown: 500
    }

  def start_link(_opts),
    do: Plug.Cowboy.http(__MODULE__, [])
end
