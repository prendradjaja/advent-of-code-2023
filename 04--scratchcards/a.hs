#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE
--   ./b.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import Control.Arrow ((>>>))
import System.Environment (getArgs)
import qualified Data.Set as Set


main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text


solve text =
  text
  & lines
  & map solveLine
  & sum


solveLine card =
  card

  -- Take only after the ':'
  & dropWhile (/= ':')
  & drop 1

  -- Split on '|' and parse ints
  & map (\c -> if c == '|' then '\n' else c)
  & lines
  & map readIntsToSets

  -- Count matches
  & \[winners, chosen] -> Set.intersection winners chosen
  & Set.size

  -- Calculate points for this card
  & \matches ->
      if matches == 0
      then 0
      else 2 ^ (matches - 1)


-- e.g. readIntsToSets "1 2 3" == Set.fromList [1, 2, 3]
readIntsToSets s =
  s
  & words
  & map readInt
  & Set.fromList

readInt = read :: String -> Int
