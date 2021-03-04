jQuery(() => {
    // アドレスバーに #Anchor があるとき, Anchor を抽出
    let hashId = location.hash && location.hash.substr(1);
    // --------------------------------------------------------------
    // タブ切り替え関数
    //      -任意のタブに tabクラスを付与すること
    //      -表示するパネルに panel-contentクラスを付与すること
    if (hashId) {
        // name 属性 == Anchor のとき
        $('.tab').each((index) => {
            // アドレスバーに #Anchor があるとき
            if ($('.tab').eq(index).attr('name') == hashId) {
                // 現在の is-active クラスを削除
                $('.is-active').removeClass('is-active');
                // 表示している要素の is-show クラスを削除
                $('.is-show').removeClass('is-show');
                // 条件を満たした tab を is-active クラスにする
                $('.tab').eq(index).addClass('is-active');
                // tab と同じインデックス番号をもつコンテンツを表示
                $('.panel-content').eq(index).addClass('is-show');
            }
        });
    }
    // --------------------------------------------------------------
    // タブ名取得関数
    //      -サイドバー専用
    $('.tab').click(function () {
        // 現在の is-active クラスを削除
        $('.is-active').removeClass('is-active');
        // クリックした tab を is-active クラスにする
        $(this).addClass('is-active');
        // 表示している要素の is-show クラスを削除
        $('.is-show').removeClass('is-show');
        // クリックしたタブからインデックス番号を取得
        const index = $(this).index();
        // クリックしたタブと同じインデックス番号をもつコンテンツを表示
        $('.panel-content').eq(index).addClass('is-show');
    });

});