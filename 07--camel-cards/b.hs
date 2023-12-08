#!/usr/bin/env runhaskell
-- Usage:
--   ./b.hs PATH_TO_INPUT_FILE

import Data.Function ((&))
import Data.List (sort, sortOn, group, elem, elemIndex, concat, maximumBy)
import Data.Maybe (fromJust)
import Data.Ord (comparing)
import System.Environment (getArgs)


data Hand = Hand
  { cards :: String
  , bid :: Int
  } deriving (Show)

-- Could be just Int, but this makes things easier to debug, since you can
-- easily print a HandType and see what it is
type HandType = (Int, String)

fiveOfAKind = (7, "fiveOfAKind") :: HandType
fourOfAKind = (6, "fourOfAKind")
fullHouse = (5, "fullHouse")
threeOfAKind = (4, "threeOfAKind")
twoPair = (3, "twoPair")
onePair = (2, "onePair")
highCard = (1, "highCard")


main = do
  [inputPath] <- getArgs
  text <- readFile inputPath
  print $ solve text

solve text =
  zip [1..] hands
  & map (\(rank, hand) -> rank * (bid hand))
  & sum
  where
    hands =
      text
      & lines
      & map words
      & map
          (\[myCards, bidString] ->
            Hand myCards (read bidString)
          )
      & sortOn
          (\hand ->
            (
              getHandType $ resolveJokers $ cards hand,
              map getCardValue $ cards hand
            )
          )

resolveJokers cards =
  maximumBy
    (comparing getHandType)
    (fillSlots cards "AKQT98765432" 'J')

fillSlots string chooseFrom slotChar
  | not (slotChar `elem` string)
    = [string]
  | otherwise
    =
      let
        idx = fromJust $ elemIndex slotChar string
      in
        concatMap
          (\choice ->
            fillSlots
              ((take idx string) ++ [choice] ++ (drop (idx + 1) string))
              chooseFrom
              slotChar
          )
          chooseFrom

getHandType myCards
  | counts == [5]
    = fiveOfAKind
  | counts == [4, 1]
    = fourOfAKind
  | counts == [3, 2]
    = fullHouse
  | counts == [3, 1, 1]
    = threeOfAKind
  | counts == [2, 2, 1]
    = twoPair
  | counts == [2, 1, 1, 1]
    = onePair
  | counts == [1, 1, 1, 1, 1]
    = highCard
  where
    counts =
      myCards
      & sort
      & group
      & map length
      & sort
      & reverse

getCardValue card
  | card == 'A' = 14
  | card == 'K' = 13
  | card == 'Q' = 12
  | card == 'T' = 10
  | card == 'J' = 1
  | otherwise   = read [card]
