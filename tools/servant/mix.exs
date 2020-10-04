defmodule Servant.MixProject do
  use Mix.Project

  def project do
    [
      app: :servant,
      version: "0.1.0",
      elixir: "~> 1.10",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {Servant.Application, []}
    ]
  end

  defp deps do
    [
      {:cowboy, "~> 2.8"},
      {:plug, "~> 1.10"}
    ]
  end
end
