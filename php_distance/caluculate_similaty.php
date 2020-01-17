<?php
    /*
    * ベクトル同士の類似度比較クラス
    * - cos_similary = コサイン類似度
    * - euclid_similary = ユークリッド距離
    * - Mahalanobis' Distance = マハラノビス距離
    * - chebyshev_distance = チェビシェフ距離
    * - ...追記
    */

    class caluculate_distance{

        /*外部向けに呼び出されるやつら*/
        public function cos_similary($ori_vec, $tar_vecs)
        {
            /*
            *$ori_vec と $tar_vecs の各ベクトルとのcos類似度の計算を行う
            */
            $res = array();

            $array_a = $this->cos_array($ori_vec);
            for ($i=0; $i < count($tar_vecs); $i++)
            {// ori_vecと各tar_vecsとの類似度計算
                // ori_vecとtar_vecs[$i]とのアダマール積の計算
                $hadamard = $this->distance_array($ori_vec, $tar_vecs[$i], 'hadamard');
                // √∑b^2_i の計算
                $array_b = $this->cos_array($tar_vecs[$i]);
                // 類似度の格納
                $res[] = array_sum($hadamard) / (sqrt(array_sum($array_a)) * sqrt(array_sum($array_b)));
            }

            return $res;
        }

        public function manhattan_distance($ori_vec, $tar_vecs)
        {
            /*
            * ori_vecに対して各tar_vevcsのマンハッタン距離を返却する
            */
            $res = array();
            for ($i = 0; $i < count($tar_vecs); $i++)
            {// ori_vecと各tar_vecsとの距離計算
                $manhattan_array = $this->distance_array($ori_vec, $tar_vecs[$i], 'manhattan');
                $res[] = array_sum($manhattan_array);
            }

            return $res;
        }

        public function euclid_distance($ori_vec, $tar_vecs)
        {
            /*
            * ori_vecに対して各tar_vecsのユークリッド距離を返却する
            */
            $res = array();
            for ($i=0;$i<count($tar_vecs);$i++)
            {
                $euclid_array = $this->distance_array($ori_vec, $tar_vecs[$i], 'euclid');
                $res[] = sqrt(array_sum($euclid_array));
            }
            return $res;
        }

        public function chebyshev_distance($ori_vec, $tar_vecs)
        {
            /*
            * ori_vecに対して各tar_vecsのチェビシェフ距離を返却する
            */
            $res = array();
            for ($i=0;$i<count($tar_vecs);$i++)
            {
                $chebyshev_array = $this->distance_array($ori_vec, $tar_vecs[$i], 'manhattan');
                $res[] = max($chebyshev_array);
            }
            return $res;
        }

        public function mahalanobis_distance($ori_vec, $tar_vecs)
        {
            /*
            * ori_vecに対して各tar_vecsのマハラノビス距離を返却する
            * 記載中
            */
            $res = array();
        }

        /* ここから private function */
        private function cos_array($array_a)
        {
            /*
            * cos類似度計算用の関数 / 行列の a^2_i を返却する
            */
            /* 行列 array_a を 二乗していく */
            $cos_array = array();
            for ($i=0;$i<count($array_a);$i++)
            {
                $cos_array[] = $array_a[$i]**2;
            }
            return $cos_array;
        }

        private function distance_array($array_a, $array_b, $type = 'euclid'){
            /*
            * $type に指定された距離の返却をする
            * $type = euclid -> ユークリッド距離
            * $type = hadamard -> アダマール積
            * $type = manhattan -> マンハッタン距離
            */
            //行列同士の長さが違う場合はそのまま返却する
            if (count($array_a) != count($array_b)){
                return None;
            }
            // type毎に返却値を変えて、$array_aと$array_bのベクトル距離を計算する
            $distance_array = array();
            for ($i = 0; $i < count($array_a); $i++){
                if ($type == 'hadamard'){
                    $distance_array[] = $this->hadamard_array($array_a[$i], $array_b[$i]);
                } elseif ($type == 'euclid') {
                    $distance_array[] = $this->euclid_array($array_a[$i], $array_b[$i]);
                } elseif ($type == 'manhattan') {
                    $distance_array[] = $this->manhattan_array($array_a[$i], $array_b[$i]);
                }
            }
            return $distance_array;
        }

        private function hadamard_array($a, $b)
        {
            /*
            * $array_a * $array_b のアダマール積の計算
            */
            return $a * $b;
        }

        private function euclid_array($a, $b)
        {
            /*
            * ユークリッド距離計算用の関数 / 行列の √∑(q_i - p_i)**2 を返却する
            */
            return ($a - $b)**2;
        }

        private function manhattan_array($a, $b)
        {
            /*
            * マンハッタン距離計算用の関数 / 行列の |a_i - b_i| を返却する
            */
            return abs($a - $b);
        }
    }
?>