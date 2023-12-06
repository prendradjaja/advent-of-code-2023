#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE
--   ./b.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import System.Environment (getArgs)


main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text


solve text =
  countWins time distance
  where
    [timesText, distancesText] = lines text

    parse line =
      line
      & words
      & drop 1
      & concat
      & readInt

    time = parse timesText
    distance = parse distancesText


countWins time recordDistance =
  [0..time]
  & map
      (\chargeTime ->
        let
          moveTime = time - chargeTime
          speed = chargeTime
        in
          speed * moveTime
      )
  & filter
      (\distance ->
        distance > recordDistance
      )
  & length


readInt = read :: String -> Int
