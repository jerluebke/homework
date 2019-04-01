std::vector<int> fibs( int n )
{
    int i;
    std::vector<int> res;

    res.push_back(1);
    res.push_back(1);
    for ( i = 2; res[i-1] < n; ++i )
        res.push_back( res[i-1] + res[i-2] );

    return res;
}
