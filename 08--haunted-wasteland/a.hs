#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import Data.List (isPrefixOf, elem)
import Data.Maybe (fromJust)
import System.Environment (getArgs)
import qualified Data.Map as Map

main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text

solve text =
  (cycle instructions)
  & scanl (applyInstruction network) "AAA"
  & takeWhile (/= "ZZZ")
  & length
  where
    [instructions, networkText] = split "\n\n" text
    network =
      networkText
      & lines
      & map
          (\line ->
            line
            & filter (\c -> not $ c `elem` "=,()")
            & words
            & \[node, left, right] ->
                (
                  node,
                  \direction ->
                    case direction of
                      'L' -> left
                      'R' -> right
                )
          )
      & Map.fromList

applyInstruction network node instruction =
  (unsafeLookup node network) instruction

unsafeLookup k myMap =
  Map.lookup k myMap
  & fromJust

split sep s = split' sep s [] ""
  where
    split' sep s parts curr
      | null s =
          parts ++ [curr]
      | sep `isPrefixOf` s =
          split'
            sep
            (drop (length sep) s)
            (parts ++ [curr])
            ""
      | otherwise =
          split'
            sep
            (tail s)
            parts
            (curr ++ [(head s)])
