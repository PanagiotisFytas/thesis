readers_rwr() ->
    ets:new(table, [public, named_table]),
    ets:insert(table, {x, 0}),
    ets:insert(table, {y, 0}),
    Writer =
        fun() ->
                ets:insert(table, {x, 1})
        end,
    Reader =
        fun() ->
                ets:lookup(table, y),
                ets:lookup(table, x)
        end,
    spawn(Reader),
    spawn(Writer),
    spawn(Reader),
    receive
    after
        infinity -> ok
    end.
