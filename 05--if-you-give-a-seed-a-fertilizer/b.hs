#!/usr/bin/env runhaskell
-- Usage:
--   ./a.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import Data.List (elemIndex, minimum)
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
  interestingSeeds
  & filter isInitialSeed
  & map seedToLocation
  & minimum
  where
    -- Parse seeds and map data
    paragraphs = split "\n\n" text
    seedsText = head paragraphs
    mapTexts = drop 1 paragraphs

    seedsData =
      seedsText
      & words
      & drop 1
      & map readInt

    seedRanges =
      seedsData
      & pairs
      & map (\(myStart, length) -> IntRange myStart (myStart + length))

    mapDatas = map parseMap mapTexts

    -- Convert to functions
    functions = map toFunction mapDatas

    -- Find interesting seeds (See b.py for explanation)
    interestingSeeds =
      foldr
        (\currMapData accInterestingValues ->
          let
            fInverse = toInverseFunction currMapData
          in
            accInterestingValues
            & (++ getInterestingValues currMapData)
            & map fInverse
        )
        []
        mapDatas

    -- Other helpers
    isInitialSeed seed =
      any
        (\range -> rangeContains range seed)
        seedRanges

    seedToLocation seed =
      foldl
        (\accValue currFn -> currFn accValue)
        seed
        functions


pairs [] = []
pairs (x:y:xs) = (x, y) : (pairs xs)


parseMap text =
  text
  & lines
  & drop 1
  & map (\line -> line & words & map readInt)


getSrcRanges mapData =
  mapData
  & map (\[_, start, length] -> IntRange start (start + length))


getDstRanges mapData =
  mapData
  & map (\[start, _, length] -> IntRange start (start + length))


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
    srcRanges = getSrcRanges mapData
    dstRanges = getDstRanges mapData


toInverseFunction mapData =
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
    dstRanges = getSrcRanges mapData
    srcRanges = getDstRanges mapData


getInterestingValues mapData =
  dstRanges
  & concatMap
      (\range -> [
        start range - 1,
        start range,
        end range - 1,
        end range
      ])
  where
    dstRanges = getDstRanges mapData


firstBy f xs =
  filter f xs
  & head


rangeContains r x =
  (start r) <= x && x < (end r)
