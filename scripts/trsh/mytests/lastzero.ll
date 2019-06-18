; ModuleID = 'lastzero.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%union.pthread_attr_t = type { i64, [48 x i8] }

@array = common global [5 x i32] zeroinitializer, align 16
@idx = common global [5 x i32] zeroinitializer, align 16

; Function Attrs: nounwind uwtable
define i8* @thread_reader(i8* %unused) #0 {
  %1 = alloca i8*, align 8
  %i = alloca i32, align 4
  store i8* %unused, i8** %1, align 8
  store i32 4, i32* %i, align 4
  br label %2

; <label>:2                                       ; preds = %9, %0
  %3 = load i32, i32* %i, align 4
  %4 = sext i32 %3 to i64
  %5 = getelementptr inbounds [5 x i32], [5 x i32]* @array, i64 0, i64 %4
  %6 = load i32, i32* %5, align 4
  %7 = icmp ne i32 %6, 0
  br i1 %7, label %8, label %12

; <label>:8                                       ; preds = %2
  br label %9

; <label>:9                                       ; preds = %8
  %10 = load i32, i32* %i, align 4
  %11 = add nsw i32 %10, -1
  store i32 %11, i32* %i, align 4
  br label %2

; <label>:12                                      ; preds = %2
  ret i8* null
}

; Function Attrs: nounwind uwtable
define i8* @thread_writer(i8* %arg) #0 {
  %1 = alloca i8*, align 8
  %j = alloca i32, align 4
  store i8* %arg, i8** %1, align 8
  %2 = load i8*, i8** %1, align 8
  %3 = bitcast i8* %2 to i32*
  %4 = load i32, i32* %3, align 4
  store i32 %4, i32* %j, align 4
  %5 = load i32, i32* %j, align 4
  %6 = sub nsw i32 %5, 1
  %7 = sext i32 %6 to i64
  %8 = getelementptr inbounds [5 x i32], [5 x i32]* @array, i64 0, i64 %7
  %9 = load i32, i32* %8, align 4
  %10 = add nsw i32 %9, 1
  %11 = load i32, i32* %j, align 4
  %12 = sext i32 %11 to i64
  %13 = getelementptr inbounds [5 x i32], [5 x i32]* @array, i64 0, i64 %12
  store i32 %10, i32* %13, align 4
  ret i8* null
}

; Function Attrs: nounwind uwtable
define i32 @main() #0 {
  %1 = alloca i32, align 4
  %t = alloca [5 x i64], align 16
  %i = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 0, i32* %i, align 4
  br label %2

; <label>:2                                       ; preds = %37, %0
  %3 = load i32, i32* %i, align 4
  %4 = icmp sle i32 %3, 4
  br i1 %4, label %5, label %40

; <label>:5                                       ; preds = %2
  %6 = load i32, i32* %i, align 4
  %7 = load i32, i32* %i, align 4
  %8 = sext i32 %7 to i64
  %9 = getelementptr inbounds [5 x i32], [5 x i32]* @idx, i64 0, i64 %8
  store i32 %6, i32* %9, align 4
  %10 = load i32, i32* %i, align 4
  %11 = icmp eq i32 %10, 0
  br i1 %11, label %12, label %24

; <label>:12                                      ; preds = %5
  %13 = load i32, i32* %i, align 4
  %14 = sext i32 %13 to i64
  %15 = getelementptr inbounds [5 x i64], [5 x i64]* %t, i64 0, i64 %14
  %16 = load i32, i32* %i, align 4
  %17 = sext i32 %16 to i64
  %18 = getelementptr inbounds [5 x i32], [5 x i32]* @idx, i64 0, i64 %17
  %19 = bitcast i32* %18 to i8*
  %20 = call i32 @pthread_create(i64* %15, %union.pthread_attr_t* null, i8* (i8*)* @thread_reader, i8* %19) #3
  %21 = icmp ne i32 %20, 0
  br i1 %21, label %22, label %23

; <label>:22                                      ; preds = %12
  call void @abort() #4
  unreachable

; <label>:23                                      ; preds = %12
  br label %36

; <label>:24                                      ; preds = %5
  %25 = load i32, i32* %i, align 4
  %26 = sext i32 %25 to i64
  %27 = getelementptr inbounds [5 x i64], [5 x i64]* %t, i64 0, i64 %26
  %28 = load i32, i32* %i, align 4
  %29 = sext i32 %28 to i64
  %30 = getelementptr inbounds [5 x i32], [5 x i32]* @idx, i64 0, i64 %29
  %31 = bitcast i32* %30 to i8*
  %32 = call i32 @pthread_create(i64* %27, %union.pthread_attr_t* null, i8* (i8*)* @thread_writer, i8* %31) #3
  %33 = icmp ne i32 %32, 0
  br i1 %33, label %34, label %35

; <label>:34                                      ; preds = %24
  call void @abort() #4
  unreachable

; <label>:35                                      ; preds = %24
  br label %36

; <label>:36                                      ; preds = %35, %23
  br label %37

; <label>:37                                      ; preds = %36
  %38 = load i32, i32* %i, align 4
  %39 = add nsw i32 %38, 1
  store i32 %39, i32* %i, align 4
  br label %2

; <label>:40                                      ; preds = %2
  ret i32 0
}

; Function Attrs: nounwind
declare i32 @pthread_create(i64*, %union.pthread_attr_t*, i8* (i8*)*, i8*) #1

; Function Attrs: noreturn nounwind
declare void @abort() #2

attributes #0 = { nounwind uwtable "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { noreturn nounwind "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind }
attributes #4 = { noreturn nounwind }

!llvm.ident = !{!0}

!0 = !{!"clang version 3.8.0-2ubuntu4 (tags/RELEASE_380/final)"}
