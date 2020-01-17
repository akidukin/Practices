<?php
require('caluculate_similaty.php');

$a = [1,2,3,4,5,6,7,8,9];
$b = [[0,0,1,6,7,3,1,8,5]
    ,[1,2,8,5,3,5,4,7,6]
    ,[4,4,1,3,5,6,8,9,9]
    ,[5,9,2,2,8,6,1,6,9]
    ,[8,5,7,1,7,9,9,2,2]
    ,[8,2,9,4,0,1,5,8,8]];

echo "計測元のベクトル\n";
print_r($a);
echo "類似度を測る対象のベクトル\n";
print_r($b);
echo "\n*....*....*\n";

$cd = new caluculate_distance();

echo "ユークリッド距離 \n";
print_r($cd->euclid_distance($a,$b));
echo "cos類似度 \n";
print_r($cd->cos_similary($a,$b));
echo "マンハッタン距離 \n";
print_r($cd->manhattan_distance($a,$b));
echo "チェビシェフ距離 \n";
print_r($cd->chebyshev_distance($a,$b));
?>