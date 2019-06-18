; ModuleID = 'lastzero2.c'
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%union.pthread_attr_t = type { i64, [48 x i8] }

@array = global [4 x i32] zeroinitializer, align 16
@idx = common global [4 x i32] zeroinitializer, align 16

; Function Attrs: nounwind uwtable
define i8* @thread_reader(i8* %unused) #0 {
  %1 = alloca i8*, align 8
  %i = alloca i32, align 4
  %2 = alloca i32, align 4
  store i8* %unused, i8** %1, align 8
  store i32 3, i32* %i, align 4
  br label %3

; <label>:3                                       ; preds = %11, %0
  %4 = load i32, i32* %i, align 4
  %5 = sext i32 %4 to i64
  %6 = getelementptr inbounds [4 x i32], [4 x i32]* @array, i64 0, i64 %5
  %7 = load atomic i32, i32* %6 acquire, align 4
  store i32 %7, i32* %2, align 4
  %8 = load i32, i32* %2, align 4
  %9 = icmp ne i32 %8, 0
  br i1 %9, label %10, label %14

; <label>:10                                      ; preds = %3
  br label %11

; <label>:11                                      ; preds = %10
  %12 = load i32, i32* %i, align 4
  %13 = add nsw i32 %12, -1
  store i32 %13, i32* %i, align 4
  br label %3

; <label>:14                                      ; preds = %3
  ret i8* null
}

; Function Attrs: nounwind uwtable
define i8* @thread_writer1() #0 {
  %c = load atomic i32, i32* getelementptr inbounds ([4 x i32], [4 x i32]* @array, i64 0, i64 0) acquire, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32 %c, i32* %b, align 4
  %d = load i32, i32* %b, align 4
  %e = add nsw i32 %d, 1
  store i32 %e, i32* %a, align 4
  %f = load i32, i32* %a, align 4
  store atomic i32 %f, i32* getelementptr inbounds ([4 x i32], [4 x i32]* @array, i64 0, i64 1) release, align 4
  ret i8* null
}

; Function Attrs: nounwind uwtable
define i8* @thread_writer2() #0 {
  %c = load atomic i32, i32* getelementptr inbounds ([4 x i32], [4 x i32]* @array, i64 0, i64 1) acquire, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32 %c, i32* %b, align 4
  %d = load i32, i32* %b, align 4
  %e = add nsw i32 %d, 1
  store i32 %e, i32* %a, align 4
  %f = load i32, i32* %a, align 4
  store atomic i32 %f, i32* getelementptr inbounds ([4 x i32], [4 x i32]* @array, i64 0, i64 2) release, align 4
  ret i8* null
}

; Function Attrs: nounwind uwtable
define i8* @thread_writer3() #0 {
  %c = load atomic i32, i32* getelementptr inbounds ([4 x i32], [4 x i32]* @array, i64 0, i64 2) acquire, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32 %c, i32* %b, align 4
  %d = load i32, i32* %b, align 4
  %e = add nsw i32 %d, 1
  store i32 %e, i32* %a, align 4
  %f = load i32, i32* %a, align 4
  store atomic i32 %f, i32* getelementptr inbounds ([4 x i32], [4 x i32]* @array, i64 0, i64 3) release, align 4
  ret i8* null
}

; Function Attrs: nounwind uwtable
define i32 @main() #0 {
  %1 = alloca i32, align 4
  %t = alloca [4 x i64], align 16
  %i = alloca i32, align 4
  store i32 0, i32* %1, align 4
  store i32 0, i32* %i, align 4
  br label %2

; <label>:2                                       ; preds = %9, %0
  %3 = load i32, i32* %i, align 4
  %4 = icmp sle i32 %3, 3
  br i1 %4, label %5, label %12

; <label>:5                                       ; preds = %2
  %6 = load i32, i32* %i, align 4
  %7 = sext i32 %6 to i64
  %8 = getelementptr inbounds [4 x i32], [4 x i32]* @array, i64 0, i64 %7
  store atomic i32 0, i32* %8 seq_cst, align 4
  br label %9

; <label>:9                                       ; preds = %5
  %10 = load i32, i32* %i, align 4
  %11 = add nsw i32 %10, 1
  store i32 %11, i32* %i, align 4
  br label %2

; <label>:12                                      ; preds = %2
  %13 = getelementptr inbounds [4 x i64], [4 x i64]* %t, i64 0, i64 0
  %14 = call i32 @pthread_create(i64* %13, %union.pthread_attr_t* null, i8* (i8*)* @thread_reader, i8* null) #3
  %15 = icmp ne i32 %14, 0
  br i1 %15, label %16, label %17

; <label>:16                                      ; preds = %12
  call void @abort() #4
  unreachable

; <label>:17                                      ; preds = %12
  %18 = getelementptr inbounds [4 x i64], [4 x i64]* %t, i64 0, i64 1
  %19 = call i32 @pthread_create(i64* %18, %union.pthread_attr_t* null, i8* (i8*)* bitcast (i8* ()* @thread_writer1 to i8* (i8*)*), i8* null) #3
  %20 = icmp ne i32 %19, 0
  br i1 %20, label %21, label %22

; <label>:21                                      ; preds = %17
  call void @abort() #4
  unreachable

; <label>:22                                      ; preds = %17
  %23 = getelementptr inbounds [4 x i64], [4 x i64]* %t, i64 0, i64 2
  %24 = call i32 @pthread_create(i64* %23, %union.pthread_attr_t* null, i8* (i8*)* bitcast (i8* ()* @thread_writer2 to i8* (i8*)*), i8* null) #3
  %25 = icmp ne i32 %24, 0
  br i1 %25, label %26, label %27

; <label>:26                                      ; preds = %22
  call void @abort() #4
  unreachable

; <label>:27                                      ; preds = %22
  %28 = getelementptr inbounds [4 x i64], [4 x i64]* %t, i64 0, i64 3
  %29 = call i32 @pthread_create(i64* %28, %union.pthread_attr_t* null, i8* (i8*)* bitcast (i8* ()* @thread_writer3 to i8* (i8*)*), i8* null) #3
  %30 = icmp ne i32 %29, 0
  br i1 %30, label %31, label %32

; <label>:31                                      ; preds = %27
  call void @abort() #4
  unreachable

; <label>:32                                      ; preds = %27
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
