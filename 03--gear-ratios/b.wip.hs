#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE
--   ./b.hs PATH_TO_INPUT_FILE

import Data.Char (isDigit)
import Data.Function ((&), on)
import Data.List (groupBy, elem, nub, sort)
import System.Environment (getArgs)
import qualified Data.Map as Map

type Position = (Int, Int)
type NumberPosition = ((Int, Int), (Int, Int))

main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text

-- TODO: Works on example input, wrong answer for puzzle input
solve text =
  gearsAndNumbers
  & map product
  & sum
  where
    myLines = lines text
    get (r, c) = myLines !! r !! c
    numberPositions = findNumbers myLines
    height = length myLines
    width = length $ head myLines
    dimensions = (height, width)
    neighbors numberPosition =
      neighborPositions dimensions numberPosition
      & map get
    getNumber numberPosition =
      numberPosition
      & positionsInNumber
      & map get
      & readInt
    gearsAndNumbers =
      numberPositions
      & concatMap
          (\numberPosition ->
            neighborPositions dimensions numberPosition
            & map
              (\neighborPosition ->
                (
                  getNumber numberPosition,
                  neighborPosition,
                  get neighborPosition
                )
              )
          )
      & filter (\(_, _, neighbor) -> '*' == neighbor)
      & map (\(number, neighborPosition, _) -> (neighborPosition, number))
      & groupBy ((==) `on` fst)
      & map (\group -> map snd group)
      & filter (\group -> length group == 2)

positionsInNumber numberPosition@((r1,c1),(r2,c2)) =
  [(r1, c) | c <- [c1..c2]]

isSymbol ch = (not $ isDigit ch) && (ch /= '.')

neighborPositions dimensions@(height, width) numberPosition =
  myPositionsInNumber
  & concatMap
      (\(r, c) ->
        [
          (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
          (r,     c - 1), (r,     c), (r,     c + 1),
          (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)
        ]
      )
  & sort
  & nub
  & filter (\pos -> not $ pos `elem` myPositionsInNumber)
  & filter inBounds
  where
    myPositionsInNumber = positionsInNumber numberPosition
    inBounds (r, c) =
      0 <= r && r < height &&
      0 <= c && c < width

findNumbers myLines =
  zip
    [0..]
    (map findNumbersInLine myLines)
  & concatMap
      (\(r, groups) ->
        map
          (\(groupStartCol, groupEndCol) ->
            ((r, groupStartCol), (r, groupEndCol)) :: NumberPosition
          )
          groups
      )

findNumbersInLine line =
  line
  & zip [0..]
  & groupBy ((==) `on` (isDigit . snd))
  & filter (\group -> isDigit (snd (head group)))
  & map (\group -> map fst group)
  & map (\group -> (head group, last group))

readInt = read :: String -> Int
