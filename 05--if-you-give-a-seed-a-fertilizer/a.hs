#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import Data.List (elemIndex)
import Data.Maybe (fromJust)
import System.Environment (getArgs)

import Util (split, readInt)


data IntRange = IntRange
  { start :: Int  -- inclusive
  , end :: Int  -- exclusive
  } deriving (Show, Eq)


main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text


solve text =
  seeds
  & map seedToLocation
  & foldr1 min
  where
    -- Parse seeds and map data
    paragraphs = split "\n\n" text
    seedsText = head paragraphs
    mapTexts = drop 1 paragraphs

    seeds =
      seedsText
      & words
      & drop 1
      & map readInt

    mapDatas = map parseMap mapTexts

    -- Convert to functions
    functions = map toFunction mapDatas

    -- Apply all functions to a seed
    seedToLocation seed =
      foldl
        (\accValue currFn -> currFn accValue)
        seed
        functions


parseMap text =
  text
  & lines
  & drop 1
  & map (\line -> line & words & map readInt)


toFunction mapData =
  (\x ->
    case (any (\range -> rangeContains range x) srcRanges) of
      True ->
        let
          srcRange = firstBy (\range -> rangeContains range x) srcRanges
          dstRange =
            elemIndex srcRange srcRanges
            & fromJust
            & (\i -> dstRanges !! i)
          idx = x - (start srcRange)
        in
          (start dstRange) + idx
      False -> x
  )
  where
    srcRanges =
      mapData
      & map (\[_, start, length] -> IntRange start (start + length))
    dstRanges =
      mapData
      & map (\[start, _, length] -> IntRange start (start + length))


firstBy f xs =
  filter f xs
  & head


rangeContains r x =
  (start r) <= x && x < (end r)
