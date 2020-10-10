defmodule Servant.DatasetHandler do
  def fetch_trajectory(user_id, trajectory_id) do
    Path.join(["../../dataset", user_id, trajectory_id])
    |> Path.expand()
    |> File.read()
  end
end
