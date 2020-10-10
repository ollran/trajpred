defmodule Servant.DatasetHandler do
  def fetch_trajectory(user_id, trajectory_id) do
    IO.puts(user_id)
    IO.puts(trajectory_id)

    Path.join(["../../dataset", user_id, trajectory_id])
    |> Path.expand()
    |> File.read()
  end
end
